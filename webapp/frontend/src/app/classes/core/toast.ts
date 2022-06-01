export class Toast {
  id: number = 0;
  header: string = '';
  body: string = '';

  warning: boolean = false;
  error: boolean = false;

  timeout: number = 60000;
}
