import {mergeStyleSets, PrimaryButton, TextField} from "@fluentui/react";
import React from "react";
import {AuthService} from "../services/auth.service";

export const Login: React.FC = () => {
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");

  const styles = mergeStyleSets({
    container: {
      display: "flex",
      flexDirection: "column",
      gap: "10px",
      alignItems: "center",
      justifyContent: "center",
      height: "100vh",
    },
  });

  const login = () => {
    AuthService.login(username, password);
  };

  return <div className={styles.container}>
    <h1>Login</h1>
    <TextField label="Username" value={username} onChange={(e, v) => setUsername(v!)}/>
    <TextField label="Password" type="password" value={password} onChange={(e, v) => setPassword(v!)}/>
    <PrimaryButton onClick={login} >Login</PrimaryButton>
  </div>
};

