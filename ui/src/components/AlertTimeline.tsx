import {DefaultButton, mergeStyleSets, TextField} from "@fluentui/react";
import React, {useEffect, useMemo} from "react";
import { Alert, AlertService } from "../services/alert.service";
import {Helpers} from "../services/helpers";
import {NoteService} from "../services/note.service";

export interface IAlertTimelineProps {
  alert: Alert;
}

interface ListItem {
  date: Date,
  message: string,
}

export const AlertTimeline: React.FC<IAlertTimelineProps> = (props) => {
  const { alert } = props;
  const [noteText, setNoteText] = React.useState('');
  const [notes, setNotes] = React.useState<ListItem[]>([]);
  const startsAt = useMemo(() => AlertService.getStartsAt(alert), [alert]);
  const endsAt = useMemo(() => AlertService.getEndsAt(alert), [alert]);

  useEffect(() => {
    NoteService.getMany(alert.id)
      .then(notes => notes.map(n => ({
        date: new Date(n.createdAt as string),
        message: n.text,
      })))
      .then(setNotes);
  }, []);

  const styles = mergeStyleSets({
    itemContainer: {
      marginTop: '16px',
      height: '100%',
    },
    item: {
      minHeight: '48px',
      width: 'calc(100% - 32px)',
      position: 'relative',
      backgroundColor: '#fff',
      boxshadow: '4px 16px 15px -3px rgba(0,0,0,0.1)',
      marginBottom: '16px',
      height: 'fit-content',
      padding: '16px',
      '& > span': {
        fontSize: '12px',
        color: '#8c8c8c',
        position: 'absolute',
        top: '16px',
        right: '16px',
      },
      '& > p': {
        margin: 0,
      },
    },
    newNote: {
      boxshadow: '4px 16px 15px -3px rgba(0,0,0,0.1)',
      marginBottom: '16px',
      border: 'none',
    },
    newNoteContainer: {
      display: 'flex',
      gap: '10px',
      '& > *': {
        flexGrow: 1,
      },
      '& > button': {
        maxWidth: '50px',
        height: 'inherit',
        marginBottom: '16px',
      },
    }
  });

  const items: ListItem[] = useMemo(() => [
    { date: startsAt ?? new Date(), message: 'Alert started' },
    { date: endsAt ?? new Date(), message: 'Alert ended' },
    ...notes
  ], [notes]);


  if (startsAt == null || endsAt == null) return null;

  const onChangeNoteText = (_: any, newValue?: string) => {
    if (newValue == null) return;
    setNoteText(newValue);
  }

  const onSubmitNote = () => {
    NoteService.create({
      alertId: alert.id,
      text: noteText,
      createdAt: new Date().toISOString(),
    }).then(r => setNotes([...notes, {
      date: new Date(r.createdAt as string),
      message: r.text,
    }]));
    setNoteText('');
  }

  return <div className={styles.itemContainer}>
    <div className={styles.newNoteContainer}>
      <TextField 
        multiline 
        rows={4} 
        value={noteText} 
        onChange={onChangeNoteText} 
        className={styles.newNote}
        placeholder="Add a note..." />
      <DefaultButton iconProps={{ iconName: 'Add' }} onClick={onSubmitNote} />
    </div>
    {items
      .sort((a, b) => b.date.getTime() - a.date.getTime())
      .map(i => <div className={styles.item}>
      <span>{Helpers.formatDate(i.date)}</span>
      <p>{i.message}</p>
    </div>)}
  </div>
}

