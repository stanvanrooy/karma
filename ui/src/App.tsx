import { Navigation } from './components/Navigation';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import {mergeStyleSets} from '@fluentui/react';
import {AlertOverview} from './pages/AlertOverview';


export const App: React.FunctionComponent = () => {
  const styles = mergeStyleSets({
    contentContainer: {
      display: 'flex',
      minHeight: '100vh',
      height: '100%',
      '& > *': {
        flexGrow: 1,
      },
    },
    content: {
      padding: '0 16px',
      backgroundColor: '#f4f4f4',
    },
    navigation: {
      width: '100%',
    },
    navigationContainer: {
      maxWidth: '280px'
    }
  });

  return <div className={styles.contentContainer}>
    <BrowserRouter>
      <div className={styles.navigationContainer}>
        <Navigation className={styles.navigation} />
      </div>
      <div className={styles.content}>
        <Routes>
          <Route path="alerts" element={<AlertOverview />} />
      </Routes>
      </div>
    </BrowserRouter>
  </div>
};

