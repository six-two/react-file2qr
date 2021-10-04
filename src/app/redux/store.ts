import { createStore } from 'redux';
import { reducer } from './reducer';

export interface ReduxState {
  chunk_size: number,
  file_name: string | null,
  file_bytes: Uint8Array | null,
  error_correction_level: string,
  error_message: string | null,
  qr_data_url: string | null,
  qr_index: number,
  result_bytes: Uint8Array | null,
}


export const FALLBACK_STATE: ReduxState = {
  chunk_size: 2000,
  file_name: null,
  file_bytes: null,
  error_correction_level: "L",
  error_message: null,
  qr_data_url: null,
  qr_index: 0,
  result_bytes: null,
}

let devTools = undefined;
if ((window as any).__REDUX_DEVTOOLS_EXTENSION__) {
  // Redux dev tools are available
  let devToolOptions = {
    trace: false,
    traceLimit: 25
  };
  devTools = (window as any).__REDUX_DEVTOOLS_EXTENSION__(devToolOptions);
}

export const store = createStore(reducer, FALLBACK_STATE, devTools);

export default store;
