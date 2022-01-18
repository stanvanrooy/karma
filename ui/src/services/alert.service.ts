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

  public static get(id: number): Promise<Alert> {
    return fetch(`${BASE_API_URL}/alert/${id}`)
      .then(response => response.json());
  }

  public static count(): Promise<number> {
    return fetch(`${BASE_API_URL}/alert/count`)
      .then(r => r.json())
      .then(r => r.count);
  }

  public static update(alert: Alert): Promise<Response> {
    return fetch(`${BASE_API_URL}/alert/${alert.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(alert)
    });
  }

  public static delete(id: number): Promise<Response> {
    return fetch(`${BASE_API_URL}/alert/${id}`, {
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

