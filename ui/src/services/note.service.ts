import {BASE_API_URL} from "../constants";
import {secureFetch} from "./secureFetch";

export interface Note {
  id?: string;
  alertId: string;
  text: string;
  createdAt?: string;
}

export class NoteService {
  public static create(note: Note): Promise<Note> {
    return secureFetch(`${BASE_API_URL}/1/note`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(note)
    });
  }

  public static getMany(id: string): Promise<Note[]> {
    return secureFetch(`${BASE_API_URL}/1/alert/${id}/notes`);
  }

  public static get(id: string): Promise<Note> {
    return secureFetch(`${BASE_API_URL}/1/note/${id}`);
  }

  public static count(): Promise<number> {
    return secureFetch(`${BASE_API_URL}/1/note/count`)
      .then(r => r.count);
  }
}

