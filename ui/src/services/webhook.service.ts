import {BASE_API_URL} from "../constants";
import {secureFetch} from "./secureFetch";


export interface Webhook {
  id: string;
  name: string;
}


export class WebhookService {
  public static getMany(skip?: number, limit?: number): Promise<Webhook[]> {
    return secureFetch(`${BASE_API_URL}/1/webhook?skip=${skip}&limit=${limit}`);
  }

  public static count(): Promise<number> {
    return secureFetch(`${BASE_API_URL}/1/webhook/count`)
      .then(r => r.count);
  }

  public static create(): Promise<Webhook> {
    return secureFetch(`${BASE_API_URL}/1/webhook`, {
      method: 'POST',
      body: JSON.stringify({})
    });
  }

  public static delete(id: string): Promise<void> {
    return secureFetch(`${BASE_API_URL}/1/webhook${id}`, {
      method: 'DELETE'
    });
  }
}

