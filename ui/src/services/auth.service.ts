import {BASE_API_URL} from "../constants";


export class AuthService {
  public static login(username: string, password: string) {
    return fetch(`${BASE_API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username,
        password
      })
    })
    .then(response => response.json())
    .then(this.setTokens);
  }

  public static getAccessToken() {
    return localStorage.getItem('access_token');
  }

  private static setTokens(response: any) {
    localStorage.setItem('access_token', response.token);
    localStorage.setItem('refresh_token', response.refresh_token);
  }
}

