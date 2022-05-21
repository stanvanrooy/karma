import {AuthService} from "./auth.service";

export const secureFetch = (url: string, options: RequestInit = {}) => {
  const headers = new Headers();
  headers.append('Content-Type', 'application/json');
  headers.append('Accept', 'application/json');
  headers.append('Authorization', `Bearer ${AuthService.getAccessToken()}`);
  const secureOptions = { ...options, headers };
  return fetch(url, secureOptions)
    .then(response => {
      if (response.status === 401) {
        window.location.href = '/login';
      }
      return response.json();
    }
  );
}

