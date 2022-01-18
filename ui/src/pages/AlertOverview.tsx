import {mergeStyleSets} from "@fluentui/react";
import React, {useEffect, useMemo} from "react";
import {AlertCard} from "../components/AlertCard";
import {Pagination} from "../components/Pagination";
import {Alert, AlertService} from "../services/alert.service";


export const AlertOverview: React.FC = () => {
  const [limit, setLimit] = React.useState(5);
  const [skip, setSkip] = React.useState(0);
  const [count, setCount] = React.useState(0);
  const [alerts, setAlerts] = React.useState<Alert[]>([]);

  useEffect(() => {
    AlertService.count().then(setCount);
  }, []);

  useEffect(() => {
    AlertService.getMany(skip, limit).then(setAlerts);
  }, [skip, limit]);

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
  });

  return <div>
    <div className={styles.header}>
      <h1>Alerts</h1>
      <Pagination count={count} skip={skip} limit={limit} onPageChange={setSkip} onLimitChange={setLimit} />
    </div>
    {alertCards}
  </div>;
}

