import {BASE_API_URL} from "../constants";
import {secureFetch} from "./secureFetch";

export interface Note {
  id?: number;
  alertId: number;
  text: string;
  createdAt?: string;
}

export class NoteService {
  public static create(note: Note): Promise<Note> {
    return secureFetch(`${BASE_API_URL}/note`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(note)
    });
  }

  public static getMany(id: number): Promise<Note[]> {
    return secureFetch(`${BASE_API_URL}/alert/${id}/notes`);
  }

  public static get(id: number): Promise<Note> {
    return secureFetch(`${BASE_API_URL}/note/${id}`);
  }

  public static count(): Promise<number> {
    return secureFetch(`${BASE_API_URL}/note/count`)
      .then(r => r.count);
  }
}

