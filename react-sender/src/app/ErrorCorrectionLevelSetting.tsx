import { connect } from 'react-redux';
import { ReduxState } from './redux/store';
import { setErrorCorrectionLevel } from './redux/actions';
import DropdownChooser from './Dropdown';

const ERROR_CORRECTION_LEVELS = new Map<string, string>();
ERROR_CORRECTION_LEVELS.set("L", "Low (~7%)");
ERROR_CORRECTION_LEVELS.set("M", "Medium (~15%)");
ERROR_CORRECTION_LEVELS.set("Q", "Quartile (~25%)");
ERROR_CORRECTION_LEVELS.set("H", "High (~30%)");


const mapStateToProps = (state: ReduxState, ownProps: any) => {
    return {
      ...ownProps,
      value: state.error_correction_level,
      onValueChange: setErrorCorrectionLevel,
      optionMap: ERROR_CORRECTION_LEVELS,
    };
  };
  
export default connect(mapStateToProps)(DropdownChooser);
