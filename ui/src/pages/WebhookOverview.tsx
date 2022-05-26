import {mergeStyleSets, PrimaryButton} from "@fluentui/react";
import React, {useEffect, useMemo} from "react";
import {Pagination} from "../components/Pagination";
import {WebhookCard} from "../components/WebhookCard";
import {Webhook, WebhookService} from "../services/webhook.service";

export const WebhookOverview: React.FC = () => {
  const [limit, setLimit] = React.useState(5);
  const [skip, setSkip] = React.useState(0);
  const [count, setCount] = React.useState(0);
  const [webhooks, setWebhooks] = React.useState<Webhook[]>([]);

  useEffect(() => {
    WebhookService.count().then(setCount);
  }, []);

  useEffect(() => {
    WebhookService.getMany(skip, limit).then(setWebhooks);
  }, [skip, limit]);

  const styles = mergeStyleSets({
    header: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      position: "sticky",
      top: 0,
    },
  });

  const onDelete = (webhook: Webhook) => {
    WebhookService.delete(webhook.id).then(() => {
      console.log("deleted");
      setWebhooks(webhooks.filter(w => w.id !== webhook.id));
    });
  };

  const addWebhook = () => {
    WebhookService.create().then(w => setWebhooks([...webhooks, w]));
  };

  const webhookCards = useMemo(() => webhooks.map(w => <WebhookCard 
    webhook={w} 
    key={w.id}
    onDelete={onDelete}
  />), [webhooks]);
  
  return <div>
    <div className={styles.header}>
      <h1>Webhooks</h1>
      <Pagination count={count} skip={skip} limit={limit} onPageChange={setSkip} onLimitChange={setLimit} />
    </div>
    {webhookCards}

    <PrimaryButton 
      text="Add Webhook" 
      onClick={() => addWebhook()} 
      style={{width: "100%"}}
    />
  </div>
};

