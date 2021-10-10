import { createStore } from 'redux';
import { HashedData } from '../encoders/QrHeaders';
import { reducer } from './reducer';

export interface ReduxState {
  chunks: ChunkState,
  error_correction_level: string,
  error_message: string | null,
  file: FileState | null,
  slide_show: SlideShowState,
}

export interface SlideShowState {
  enabled: boolean,
  // for how many milliseconds a slide should be shown
  time_in_ms: number,
}

export interface FileState {
  name: string,
  contents: Uint8Array,
  serialized: HashedData,
}

export interface ChunkState {
  // how big each of the chunks are (without headers)
  size: number,
  // the index of the chunk to show
  index: number,
  // index of the last chunk
  max_index: number,
}

export const FALLBACK_STATE: ReduxState = {
  chunks: {
    size: 2000,
    index: 0,
    max_index: 0,
  },
  error_correction_level: "L",
  error_message: null,
  file: null,
  slide_show: {
    enabled: false,
    time_in_ms: 1000,
  }
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
