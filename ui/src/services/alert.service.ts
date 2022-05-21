import {BASE_API_URL} from "../constants";
import {secureFetch} from "./secureFetch";

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
  public static getMany(skip?: number, limit?: number, query?: string): Promise<Alert[]> {
    return secureFetch(`${BASE_API_URL}/alert?skip=${skip}&limit=${limit}&query=${query}`);
  }

  public static get(id: number): Promise<Alert> {
    return secureFetch(`${BASE_API_URL}/alert/${id}`);
  }

  public static count(query?: string): Promise<number> {
    return secureFetch(`${BASE_API_URL}/alert/count?query=${query}`)
      .then(r => r.count);
  }

  public static update(alert: Alert): Promise<Response> {
    return secureFetch(`${BASE_API_URL}/alert/${alert.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(alert)
    });
  }

  public static delete(id: number): Promise<Response> {
    return secureFetch(`${BASE_API_URL}/alert/${id}`, {
      method: 'DELETE'
    });
  }

  public static getTitle(alert?: Alert): string | null {
    if (!alert) {
      return null;
    }
    return alert.labels.alertname ?? "No title";
  }

  public static getSummary(alert?: Alert): string | null{
    if (!alert) {
      return null;
    }
    return alert.annotations.summary ?? "No summary";
  }

  public static getDescription(alert?: Alert): string | null{
    if (!alert) {
      return null;
    }
    return alert.annotations.description ?? "No description";
  }

  public static getStartsAt(alert?: Alert): Date | null {
    if (!alert) {
      return null;
    }
    return new Date(alert.startsAt);
  }

  public static getEndsAt(alert?: Alert): Date | null {
    if (!alert) {
      return null;
    }
    return new Date(alert.endsAt);
  }

  public static getStatus(alert?: Alert): string | null {
    if (!alert) {
      return null;
    }
    switch(alert.status) {
      case "firing":
        return "Firing";
      case "resolved":
        return "Resolved";
      case "in-review":
        return "In review";
      default: 
        throw new Error(`Unknown status: ${alert.status}`);
    }
  }
}

