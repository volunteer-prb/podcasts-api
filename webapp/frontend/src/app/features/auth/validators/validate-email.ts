import { FormControl } from '@angular/forms';

export function validateEmail(c: FormControl) {
  const EMAIL_REGEXP =
    // eslint-disable-next-line max-len
    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,5}))$/;

  return EMAIL_REGEXP.test(c.value)
    ? null
    : {
        validateEmail: {
          valid: false,
        },
      };
}
