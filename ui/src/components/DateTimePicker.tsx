import {DatePicker, Label, mergeStyleSets, TextField} from "@fluentui/react";
import React, {useMemo} from "react";

export interface IDateTimePickerProps {
  label: string;
  value: Date;
  onChangeDate: (value: Date) => void;
}

export const DateTimePicker: React.FC<IDateTimePickerProps> = (props) => {
  const {label, value, onChangeDate} = props;
  const hours = useMemo(() => value.getHours(), [value]);
  const minutes = useMemo(() => value.getMinutes(), [value]);

  const styles = mergeStyleSets({
    container: {
      display: 'flex',
      gap: 10,
      '& > *': {
        flexGrow: 1,
      }
    },
    datePicker: {
      minWidth: '50%',
    }
  });

  const onChange = (date: Date | null | undefined) => {
    if (!date) {
      return;
    }
    onChangeDate(date);
  };

  const onChangeHours = (_: any, v?: string) => {
    if (!v) {
      return;
    }

    let hours = parseInt(v);
    if (hours === 24) {
      hours = 0
    } else if (hours === -1) {
      hours = 23;
    }
    const date = new Date(value.getTime());
    date.setHours(hours);
    onChangeDate(date);
  }

  const onChangeMinutes = (_: any, v?: string) => {
    if (!v) {
      return;
    }

    let minutes = parseInt(v);
    if (minutes === 60) {
      minutes = 0;
    } else if (minutes === -1) {
      minutes = 59;
    }

    const date = new Date(value.getTime());
    date.setMinutes(minutes);
    onChangeDate(date);
  }

  return <div>
    <Label>{label}</Label>
    <div className={styles.container}>
      <DatePicker
        className={styles.datePicker}
        value={value}
        onSelectDate={onChange}
      />
      <TextField 
        type="number"
        value={hours.toString()}
        onChange={onChangeHours}
      />
      <TextField 
        type="number"
        value={minutes.toString()}
        onChange={onChangeMinutes}
      />
    </div>
  </div>
}

