import { connect } from 'react-redux';
import { ChunkState, ReduxState } from './redux/store';
import { setChunkIndex } from './redux/actions';

export const INDEX_NEXT = -1;
export const INDEX_PREV = -2;

const ChangeIndexButton = (props: Props) => {
    let new_index = props.index;
    const old_index = props.chunks.index;
    let text = `${old_index}`;

    if (new_index === INDEX_NEXT) {
        new_index = old_index + 1;
        text = ">";
    } else if (new_index === INDEX_PREV) {
        new_index = old_index - 1;
        text = "<";
    }
    const enabled = 0 <= new_index && new_index <= props.chunks.max_index;
    return <button
        className="index-button"
        disabled={!enabled}
        onClick={() => setChunkIndex(new_index)}>
        {text}
    </button>
};

interface Props {
    index: number,
    chunks: ChunkState,
}

const mapStateToProps = (state: ReduxState, ownProps: any) => {
    return {
        ...ownProps,
        chunks: state.chunks,
    };
};

export default connect(mapStateToProps)(ChangeIndexButton);
