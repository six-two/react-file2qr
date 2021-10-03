import ErrorCorrectionLevelSetting from './ErrorCorrectionLevelSetting';
import '../App.css';
import QRCodeImage from './QRCodeImage';
import FileChooser from './FileChooser';
import ErrorMessage from './ErrorMessage';

function App() {
  return (
    <div className="App">
      <div>
        <FileChooser />
        <ErrorCorrectionLevelSetting />
        <ErrorMessage />
      </div>
      <QRCodeImage />
    </div>
  );
}

export default App;
