import {BASE_API_URL} from "../constants";

export interface Alert {
  id: number;
  annotations: any;
  labels: any;
  startsAt: string;
  endsAt: string;
  status: string;
  generatorUrl: string;
}

export class AlertService {
  public static getMany(skip?: number, limit?: number): Promise<Alert[]> {
    return fetch(`${BASE_API_URL}/alert?skip=${skip}&limit=${limit}`)
      .then(response => response.json());
  }

  public static count(): Promise<number> {
    return fetch(`${BASE_API_URL}/alert/count`)
      .then(r => r.json())
      .then(r => r.count);
  }
}

