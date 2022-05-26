import {mergeStyleSets} from '@fluentui/react';
import React, {useMemo} from 'react';
import {Alert, AlertService} from '../services/alert.service';
import {Label} from './Label';
import {useNavigate} from 'react-router-dom';
import {Helpers} from '../services/helpers';
import {common} from './styles';

export interface IAlertCardProps {
  alert: Alert;
}

export const AlertCard: React.FC<IAlertCardProps> = (props) => {
  const {alert} = props;

  const styles = mergeStyleSets(common, {
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

  const title = useMemo(() => AlertService.getTitle(alert), [alert]);
  const summary = useMemo(() => AlertService.getSummary(alert), [alert]);
  const date = useMemo(() => Helpers.formatDate(AlertService.getStartsAt(alert)), [alert]);
  const status = useMemo(() => AlertService.getStatus(alert), [alert]);

  const labels = useMemo(() => {
    return Object.keys(alert.labels)
      .sort((a, b) => a.localeCompare(b))
      .map(k => <Label label={k} value={alert.labels[k]} key={k} />);
  }, [alert]);

  const navigate = useNavigate();
  const openDetails = () => {
    navigate(`/alerts/${alert.id}`);
  }

  return <div onClick={_ => openDetails()} className={styles.card}>
    <div className={styles.headerContainer}>
      <h2>{title} ({status})</h2>
      <span className={'date'}>{date}</span>
    </div>
    <span>{summary}</span>

    <div className={styles.labelContainer}>
      {labels}
    </div>
  </div>
}

