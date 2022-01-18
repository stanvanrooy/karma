import {mergeStyleSets} from '@fluentui/react';
import React, {useMemo} from 'react';
import {Alert} from '../services/alert.service';
import {Label} from './Label';
import {useNavigate} from 'react-router-dom';

export interface IAlertCardProps {
  alert: Alert;
}

export const AlertCard: React.FC<IAlertCardProps> = (props) => {
  const {alert} = props;

  const styles = mergeStyleSets({
    alertCard: {
      boxShadow: '4px 16px 15px -3px rgba(0,0,0,0.1)',
      marginBottom: '16px',
      padding: '16px',
      backgroundColor: '#fff',
      cursor: 'pointer',
      display: 'flex',
      flexDirection: 'column',
      gap: '16px',
    },
    labelContainer: {
      display: 'flex',
      flexDirection: 'row',
      gap: 10,
    },
    headerContainer: {
      display: 'flex',
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      '& > h2': {
        margin: '0',
      },
      '& > .date': {
        fontSize: '12px',
        color: '#8c8c8c',
      },
    },
  });

  const title = useMemo(() => {
    return alert.labels.alertname ?? "No title";
  }, [alert]);

  const summary = useMemo(() => {
    return alert.annotations.summary ?? "No summary";
  }, [alert]);

  const date = useMemo(() => {
    const date = new Date(alert.startsAt);
    return `${date.getDate()}-${date.getMonth()}-${date.getFullYear()} ${date.getHours()}:${date.getMinutes()}`;
  }, [alert]);

  const labels = useMemo(() => {
    return Object.keys(alert.labels)
      .sort((a, b) => a.localeCompare(b))
      .map(k => <Label label={k} value={alert.labels[k]} key={k} />);
  }, [alert]);

  const navigate = useNavigate();
  const openDetails = () => {
    navigate(`/alerts/${alert.id}`);
  }

  return <div onClick={_ => openDetails()} className={styles.alertCard}>
    <div className={styles.headerContainer}>
      <h2>{title}</h2>
      <span className={'date'}>{date}</span>
    </div>
    <span>{summary}</span>

    <div className={styles.labelContainer}>
      {labels}
    </div>
  </div>
}

