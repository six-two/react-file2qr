import { HashedData, serializeFile } from '../encoders/QrHeaders';
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
      return updateChunks({
        ...state,
        error_correction_level: action.payload as string,
      });
    }
    case C.SET_ERROR_MESSAGE: {
      return {
        ...state,
        error_message: action.payload as string,
      };
    }
    case C.SET_CHUNK_INDEX: {
      let index = action.payload as number;
      const old_index = state.chunks.index;
      if (index === C.INDEX_NEXT) {
        index = (old_index < state.chunks.max_index) ? old_index + 1 : 0;
      } else if (index === C.INDEX_PREV) {
        index = (old_index > 0) ? old_index - 1 : state.chunks.max_index;
      }
      return {
        ...state,
        chunks: {
          ...state.chunks,
          index: index,
        },
      };
    }
    case C.SET_FILE: {
      const payload = action.payload as Actions.FilePayload;
      const serialized = serializeFile(payload.file_name, payload.file_bytes);
      return updateChunks({
        ...state,
        file: {
          name: payload.file_name,
          contents: payload.file_bytes,
          serialized: new HashedData(serialized),
        }
      });
    }
    case C.SET_SLIDE_SHOW_ENABLED: {
      return {
        ...state,
        slide_show: {
          ...state.slide_show,
          enabled: action.payload as boolean,
        },
      };
    }
    default: {
      console.log("Unknown action", action.type);
      return state;
    }
  }
}

const updateChunks = (state: ReduxState) => {
  const size = state.chunks.size;
  let chunk_count = 1;
  if (state.file) {
    chunk_count = Math.ceil(state.file?.serialized.data.length / size);
  }
  return {
    ...state,
    chunks: {
      size: size,
      index: 0,
      max_index: chunk_count - 1,
    }
  };
}

export default reducer;
