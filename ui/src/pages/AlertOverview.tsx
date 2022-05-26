import {mergeStyleSets, TextField} from "@fluentui/react";
import React, {useEffect, useMemo} from "react";
import {AlertCard} from "../components/AlertCard";
import {Pagination} from "../components/Pagination";
import {Alert, AlertService} from "../services/alert.service";


export const AlertOverview: React.FC = () => {
  const [limit, setLimit] = React.useState(5);
  const [skip, setSkip] = React.useState(0);
  const [count, setCount] = React.useState(0);
  const [alerts, setAlerts] = React.useState<Alert[]>([]);
  const [query, setQuery] = React.useState("");

  useEffect(() => {
    AlertService.count(query).then(setCount);
  }, []);

  useEffect(() => {
    AlertService.getMany(skip, limit, query).then(setAlerts);
  }, [skip, limit, query]);

  const alertCards = useMemo(
    () => alerts.map(alert => <AlertCard alert={alert} key={alert.id} />),
    [alerts]
  );

  const styles = mergeStyleSets({
    header: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      position: "sticky",
      top: 0,
    },
    searchContainer: {
      display: "flex",
      alignItems: "center",
      gap: 10,
    },
    searchInput: {
      minWidth: '300px',
    },
  });

  return <div>
    <div className={styles.header}>
      <div className={styles.searchContainer}>
        <h1>Alerts</h1>
        <TextField 
          className={styles.searchInput}
          placeholder="Search: e.g. env=prod, status=in-review"
          onKeyUp={(e) => {
            if (e.key !== "Enter") return;
            setQuery((e.target as any).value);
          }}
        />
      </div>
      <Pagination count={count} skip={skip} limit={limit} onPageChange={setSkip} onLimitChange={setLimit} />
    </div>
    {alertCards}
  </div>;
}

