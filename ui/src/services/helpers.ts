export class Helpers {
  public static formatDate(date: Date | null): string {
    if (date == null) {
      return '';
    }
    return `${date.getDate()}-${date.getMonth()}-${date.getFullYear()} ${date.getHours()}:${date.getMinutes()}`;
  }
}

