import { Inject, Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { LoggerService } from '../logger.service';
import { API_BASE_URL } from './rest.tokens';

export class RestOptions {
  filters: any;
  includes: string[] = [];
  order_by: any;
}

@Injectable({
  providedIn: 'root',
})
export class RestService {
  constructor(
    private http: HttpClient,
    private logger: LoggerService,
    @Inject(API_BASE_URL) private readonly baseUrl: string
  ) {}

  private includes(values: string[] | undefined): {} {
    if (values === undefined) return {};
    return values
      .map((s) => 'include_' + s)
      .map((v) => {
        let tmp: any = {};
        tmp[v] = true;
        return tmp;
      })
      .reduce((a, b) => Object.assign({}, a, b), {});
  }

  private filters(values: any): {} {
    if (values === undefined) return {};
    let filters: any = {};
    for (let key in values) {
      if (key == '_type') filters['filter_type'] = values[key];
      else filters['filter_by_' + key] = values[key];
    }
    return filters;
  }

  private order_by(values: any): {} {
    if (values === undefined) return {};
    let order_by: any = {};
    for (let key in values) {
      order_by['order_by_' + key] = values[key];
    }
    return order_by;
  }

  post(method: string, params: any = {}): Observable<any> {
    return this.request('POST', method, params);
  }

  put(method: string, params: any = {}): Observable<any> {
    return this.request('PUT', method, params);
  }

  delete(method: string, params: any = {}): Observable<any> {
    return this.request('DELETE', method, params);
  }

  get(
    method: string,
    params: any = {},
    options: RestOptions | undefined = undefined
  ): Observable<any> {
    if (options === undefined) options = new RestOptions();
    return this.request(
      'GET',
      method,
      Object.assign(
        {},
        params,
        this.includes(options.includes),
        this.filters(options.filters),
        this.order_by(options.order_by)
      ),
      null
    );
  }

  upload(method: string, fileKey: string, file: File): Observable<any> {
    const formData: FormData = new FormData();
    formData.append(fileKey, file, file.name);
    return this.request('UPLOAD', method, formData, null);
  }

  download(method: string): Observable<Blob> {
    if (!method.startsWith('/')) {
      method = '/' + method;
    }
    let httpMethod = 'GET';
    this.logger.info('Download', httpMethod, method);
    const url = this.baseUrl + method;
    return this.http.request(httpMethod, url, {
      responseType: 'blob',
    });
  }

  request(
    httpMethod: 'POST' | 'GET' | 'PUT' | 'DELETE' | 'UPLOAD',
    method: string,
    params: any,
    contentType: string | null = 'application/json; charset=UTF-8'
  ): Observable<any> {
    if (!method.startsWith('/')) {
      method = '/' + method;
    }
    this.logger.info(
      'Call rest method ',
      httpMethod,
      method,
      'with params',
      params
    );
    const url = this.baseUrl + method;
    const options: {
      headers: HttpHeaders;
      withCredentials: boolean;
      params: any | undefined;
      body: any | undefined;
    } = {
      body: undefined,
      params: undefined,
      headers:
        contentType != null
          ? new HttpHeaders({
              'Content-Type': contentType,
            })
          : new HttpHeaders(),
      withCredentials: true,
    };
    if (httpMethod === 'GET') {
      options['params'] = params;
    } else {
      options['body'] = params;
    }

    if (httpMethod === 'UPLOAD') {
      httpMethod = 'POST';
    }

    if (httpMethod === 'PUT' && params.id === undefined) {
      this.logger.warn('In rest PUT method must be `id` field in object.');
    }

    return this.http.request(httpMethod, url, options).pipe(
      map((value: any) => {
        if (value.status !== 'success') {
          this.logger.error(
            'Rest error',
            value,
            'method',
            httpMethod,
            method,
            'with params',
            params
          );
          throw value;
        }
        if (value.data === undefined) {
          this.logger.error(
            'Rest return no data',
            value,
            'method',
            httpMethod,
            method,
            'with params',
            params
          );
          throw { status: 'error', message: 'Result does not contains data' };
        }
        this.logger.info(
          'Rest response',
          value,
          'method',
          httpMethod,
          method,
          'with params',
          params
        );
        return value.data;
      })
    );
  }
}
