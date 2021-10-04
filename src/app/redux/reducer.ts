import { serializeFile } from '../encoders/QrHeaders';
import * as Actions from './actions';
import * as C from './constants';
import {
  ReduxState, FALLBACK_STATE
} from './store';

export function reducer(state: ReduxState | undefined, action: Actions.Action): ReduxState {
  if (!state) {
    console.warn("No state was supplied to reducer. Falling back to default values");
    state = FALLBACK_STATE;
  }

  switch (action.type) {
    case C.SET_ERROR_CORRECTION_LEVEL: {
      return {
        ...state,
        error_correction_level: action.payload as string,
      };
    }
    case C.SET_ERROR_MESSAGE: {
      return {
        ...state,
        error_message: action.payload as string,
      };
    }
    case C.SET_FILE: {
      const payload = action.payload as Actions.FilePayload;
      return {
        ...state,
        file_name: payload.file_name,
        file_bytes: payload.file_bytes,
        result_bytes: serializeFile(payload.file_name, payload.file_bytes),
      };
    }
    case C.SET_QR_DATA_URL: {
      return {
        ...state,
        qr_data_url: action.payload as string,
      };
    }

    default: {
      console.log("Unknown action", action.type);
      return state;
    }
  }
}

export default reducer;
