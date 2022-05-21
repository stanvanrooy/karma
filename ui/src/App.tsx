import { Navigation } from './components/Navigation';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import {mergeStyleSets} from '@fluentui/react';
import {AlertOverview} from './pages/AlertOverview';
import {AlertDetail} from './pages/AlertDetail';
import {Login} from './pages/Login';


export const App: React.FunctionComponent = () => {
  const styles = mergeStyleSets({
    contentContainer: {
      display: 'flex',
      '& > *': {
        flexGrow: 1,
      },
    },
    content: {
      padding: '0 16px',
      backgroundColor: '#f4f4f4',
      minHeight: '100vh',
    },
    navigation: {
      width: '100%',
    },
    navigationContainer: {
      maxWidth: '280px',
      position: 'sticky',
      top: 0,
      height: '100%',
    }
  });

  return <div className={styles.contentContainer}>
    <div className={styles.navigationContainer}>
      <Navigation className={styles.navigation} />
    </div>
    <BrowserRouter>
      <div className={styles.content}>
        <Routes>
          <Route path="alerts" element={<AlertOverview />} />
          <Route path="alerts/:id" element={<AlertDetail />} />
          <Route path="login" element={<Login />} />
        </Routes>
      </div>
    </BrowserRouter>
  </div>
};

