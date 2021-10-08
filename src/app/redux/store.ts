import { createStore } from 'redux';
import { reducer } from './reducer';

export interface ReduxState {
  chunk_size: number,
  error_correction_level: string,
  error_message: string | null,
  qr_index: number,
  file: FileState | null,
}

export interface FileState {
  name: string,
  contents: Uint8Array,
  serialized: Uint8Array,
}


export const FALLBACK_STATE: ReduxState = {
  chunk_size: 2000,
  error_correction_level: "L",
  error_message: null,
  qr_index: 0,
  file: null,
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
