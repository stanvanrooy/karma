import {BASE_API_URL} from "../constants";

export interface Note {
  id?: number;
  alertId: number;
  text: string;
  createdAt?: string;
}

export class NoteService {
  public static create(note: Note): Promise<Note> {
    return fetch(`${BASE_API_URL}/note`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(note)
    }).then(response => response.json());
  }

  public static getMany(id: number): Promise<Note[]> {
    return fetch(`${BASE_API_URL}/alert/${id}/notes`)
      .then(response => response.json());
  }

  public static get(id: number): Promise<Note> {
    return fetch(`${BASE_API_URL}/note/${id}`)
      .then(response => response.json());
  }

  public static count(): Promise<number> {
    return fetch(`${BASE_API_URL}/note/count`)
      .then(r => r.json())
      .then(r => r.count);
  }
}

