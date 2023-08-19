import ErrorCorrectionLevelSetting from './ErrorCorrectionLevelSetting';
import '../App.css';
import QRCodeImage from './QRCodeImage';
import FileChooser from './FileChooser';
import ErrorMessage from './ErrorMessage';
import ChangeIndexButton from './ChangeIndexButton';
import SlideShowButton from './SlideShowButton';
import { INDEX_NEXT, INDEX_PREV } from './redux/constants';

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
      <SlideShowButton />
    </div>
  );
}

export default App;
