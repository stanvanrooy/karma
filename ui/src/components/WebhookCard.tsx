import {DefaultButton, Icon, mergeStyleSets, TextField} from "@fluentui/react";
import React, {useMemo} from "react";
import {Webhook} from "../services/webhook.service";
import {common} from "./styles";

export interface IWebhookCardProps {
  webhook: Webhook,
  onDelete: (webhook: Webhook) => void,
}

export const WebhookCard: React.FC<IWebhookCardProps> = (props) => {
  const { webhook, onDelete } = props;

  const styles = mergeStyleSets(common, 
  {
    container: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
    },
    column: {
      display: "flex",
      flexGrow: 1,
      justifyContent: "end",
      gap: 10
    },
    url: {
      width: "75%",
    }
  });

  const webhookUrl = useMemo(() => {
    return `http://localhost:5000/api/1/webhook/${webhook.id}`;
  }, [webhook]);

  const openDetails = () => {

  };

  const copyUrl = () => {
    navigator.clipboard.writeText(webhookUrl);
  };

  const renderSuffix = () => {
    return <Icon
      iconName="Copy"
      onClick={copyUrl}
      className={styles.clickable}
    />;
  };

  return <div onClick={_ => openDetails()} className={styles.card}>
    <div className={styles.container}>
      <h2>{webhook.name}</h2>
      <div className={styles.column}>
        <TextField 
          className={styles.url}
          readOnly={true}
          value={webhookUrl}
          onRenderSuffix={renderSuffix}
        />
        <DefaultButton
          iconProps={{ iconName: 'Delete' }}
          onClick={_ => onDelete(webhook)}
        />
      </div>
    </div>
  </div>
}

