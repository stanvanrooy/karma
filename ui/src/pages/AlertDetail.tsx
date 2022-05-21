import {DefaultButton, Dropdown, IDropdownOption, mergeStyleSets} from "@fluentui/react";
import React, {useEffect, useMemo} from "react";
import {useNavigate, useParams} from "react-router";
import {AlertTimeline} from "../components/AlertTimeline";
import {DateTimePicker} from "../components/DateTimePicker"; import {Alert, AlertService} from "../services/alert.service";
import {Helpers} from "../services/helpers";

export const AlertDetail: React.FC = () => {
  const { id } = useParams();
  const [alert, setAlert] = React.useState<Alert>();
  const [status, setStatus] = React.useState<string>();
  const [updateTimeout, setUpdateTimeout] = React.useState<any>();

  useEffect(() => {
    if (id == null) return;
    AlertService.get(Number(id)).then(setAlert);
  }, [id])

  useEffect(() => {
    if (alert == null) return;
    setStatus(alert.status);
  }, [alert])

  const styles = mergeStyleSets({
    panelContainer: {
      display: "flex",
      gap: '16px',
      '& > *': {
        flexGrow: 1,
        height: 'calc(100vh - 64px)',
      },
    },
    panel: {
      boxShadow: '4px 16px 15px -3px rgba(0,0,0,0.1)',
      margin: '16px 0',
      '&:first-child': {
        maxWidth: '30%',
        backgroundColor: '#fff',
      },
      padding: '16px',
      position: 'relative',
    },
    date: {
      fontSize: '12px',
      color: '#8c8c8c',
    },
    headerContainer: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      '& > h1': {
        margin: 0,
      },
    },
    footerContainer: {
      position: 'absolute',
      bottom: '16px',
    },
    labelPairs: {
      fontSize: '14px',
      width: '100%',
      '& > tbody > tr > th': {
        textAlign: 'left',
        width: '40%',
      },
    }
  });

  const title = useMemo(() => AlertService.getTitle(alert), [alert])
  const description = useMemo(() => AlertService.getDescription(alert), [alert])
  const startsAt = useMemo(() => AlertService.getStartsAt(alert), [alert?.startsAt]);
  const date = useMemo(() =>  Helpers.formatDate(startsAt), [startsAt])
  const endsAt = useMemo(() => AlertService.getEndsAt(alert), [alert?.endsAt]);

  const navigate = useNavigate();

  if (alert == null || startsAt == null || endsAt == null) return null;

  const deleteAlert = () => {
    AlertService.delete(alert.id).then(() => {
      navigate('/alerts');
    });
  }

  const statusOptions = [
    { key: 'firing', text: 'Firing' },
    { key: 'in-review', text: 'In review' },
    { key: 'resolved', text: 'Resolved' },
    { key: 'false-positive', text: 'False positive' },
  ];

  // This function 'debounces' the actual update request to send 1
  // request per second, at most, instead of sending a request for every
  // change.
  const update = (a: Alert) => {
    setAlert(a);
    clearTimeout(updateTimeout);
    const u = setTimeout(() => {
      AlertService.update(a)
        .then(r => r.json())
        .then(r => {
          setAlert(r);
        });
      }, 1000);
    setUpdateTimeout(u);
  };

  const onChangeStatus = (_: any, o?: IDropdownOption) => {
    if (o == null) return;

    setStatus(o.key as string);
    const a = { ...alert, status: o.key as string };
    update(a);
  };

  const onChangeStartsAt = (date: Date | null | undefined) => {
    if (date == null) return;
    const a = { ...alert, startsAt: date.toString() };
    update(a);
  };

  const onChangeEndsAt = (date: Date | null | undefined) => {
    if (date == null) return;
    const a = { ...alert, endsAt: date.toString() };
    update(a);
  };

  return <div className={styles.panelContainer}>
    <div className={styles.panel}>
      <div className={styles.headerContainer}>
        <h1>{title}</h1>
        <span className={styles.date}>{date}</span>
      </div>

      <div style={{minHeight: 150}}>
        <p>{description}</p>
      </div>

      <h3>Labels</h3>
      <hr />
      <table className={styles.labelPairs}>
        <tbody>
          {Object.keys(alert.labels).map(k => <tr key={k}>
              <th>{k}</th>
              <td>{alert.labels[k]}</td>
            </tr>)}
        </tbody>
      </table>
      <br />

      <h3>Details</h3>
      <hr />
      <DateTimePicker onChangeDate={onChangeStartsAt} label={"Start time"} value={startsAt} />
      <DateTimePicker onChangeDate={onChangeEndsAt} label={"End time"} value={endsAt} />
      <Dropdown 
        label={"Status"} 
        options={statusOptions}
        selectedKey={status}
        onChange={onChangeStatus}
      />

      <div className={styles.footerContainer}>
        <DefaultButton 
          iconProps={{ iconName: 'Delete' }} 
          onClick={() => deleteAlert()}
        >Delete</DefaultButton>
      </div>
    </div>

    <AlertTimeline alert={alert} />
  </div>
};
