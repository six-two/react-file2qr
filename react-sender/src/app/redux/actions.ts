//Needs to be here to prevent cyclic references
import store from './store';
import * as C from './constants';

function d(action: Action) {
  store.dispatch(action);
}

export interface Action {
  type: string,
  payload?: string | number | FilePayload | boolean,
};

export interface FilePayload {
  file_name: string,
  file_bytes: Uint8Array,
}

// action creators
export function setErrorCorrectionLevel(newValue: string) {
  d({
    type: C.SET_ERROR_CORRECTION_LEVEL,
    payload: newValue,
  });
}

export function setErrorMessage(newValue: string) {
  if (store.getState().error_message === newValue){
    console.debug("Error message is the same, skipping action dispatch");
    return;//Keep by state history clean, which simplifies debugging
  }
  d({
    type: C.SET_ERROR_MESSAGE,
    payload: newValue,
  });
}


export function setFile(file_name: string, file_bytes: Uint8Array) {
  d({
    type: C.SET_FILE,
    payload: {
      file_name: file_name,
      file_bytes: file_bytes,
    },
  });
}

export function setChunkIndex(newValue: number) {
  d({
    type: C.SET_CHUNK_INDEX,
    payload: newValue,
  });
}

export function setSlideShowEnabled(newValue: boolean) {
  d({
    type: C.SET_SLIDE_SHOW_ENABLED,
    payload: newValue,
  });
}
