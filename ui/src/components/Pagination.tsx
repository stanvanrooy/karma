import {Dropdown, IDropdownOption, mergeStyleSets} from "@fluentui/react";
import {useConst} from "@fluentui/react-hooks";
import React from "react";

export interface IPaginationProps {
  skip: number;
  limit: number;
  count: number;
  onPageChange: (skip: number) => void;
  onLimitChange: (limit: number) => void;
}

export const Pagination: React.FC<IPaginationProps> = (props) => {
  const {skip, limit, count, onPageChange, onLimitChange} = props;
  const styles = mergeStyleSets({
    pagination: {
      minWidth: "160px",
      gap: 10,
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      '& > button': {
        flexGrow: 1,
        border: 'none',
        backgroundColor: '#fff',
        padding: '0.5rem',
        cursor: 'pointer',
      },
      '& > button:disabled, button[disabled]': {
        backgroundColor: '#cccccc',
        color: '#666666'
      },
    }
  });

  const dropdownOptions = useConst(() => {
    return [
      {key: 5, text: '5'},
      {key: 10, text: '20'},
      {key: 50, text: '50'},
      {key: 100, text: '100'},
    ];
  })

  return <div className={styles.pagination}>
    <Dropdown 
      options={dropdownOptions} 
      selectedKey={limit}
      onChange={(_: any, option?: IDropdownOption): any => {
        if (!option) return;
        onLimitChange(option.key as number);
      }}
    />
    <button onClick={() => onPageChange(skip - limit)} disabled={skip === 0}>
      {"<"}
    </button>
    <button onClick={() => onPageChange(skip + limit)} disabled={skip + limit >= count}>
      {">"}
    </button>
  </div>
}

