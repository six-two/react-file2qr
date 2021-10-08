import ErrorCorrectionLevelSetting from './ErrorCorrectionLevelSetting';
import '../App.css';
import QRCodeImage from './QRCodeImage';
import FileChooser from './FileChooser';
import ErrorMessage from './ErrorMessage';
import ChangeIndexButton, {INDEX_NEXT, INDEX_PREV} from './ChangeIndexButton';

function App() {
  return (
    <div className="App">
      <div>
        <FileChooser />
        <ErrorCorrectionLevelSetting />
        <ErrorMessage />
      </div>
      <QRCodeImage />
      <ChangeIndexButton index={INDEX_PREV} />
      <ChangeIndexButton index={INDEX_NEXT} />
    </div>
  );
}

export default App;
