import { connect } from 'react-redux';
import { ReduxState } from './redux/store';
import { setChunkIndex } from './redux/actions';
import { INDEX_NEXT, INDEX_PREV } from './redux/constants';


const ChangeIndexButton = (props: Props) => {
    let new_index = props.index;
    let text;

    if (new_index === INDEX_NEXT) {
        text = ">";
    } else if (new_index === INDEX_PREV) {
        text = "<";
    } else {
        text = `${new_index}`;
    }
    return <button
        className="index-button"
        onClick={() => setChunkIndex(new_index)}>
        {text}
    </button>
};

interface Props {
    index: number,
}

const mapStateToProps = (state: ReduxState, ownProps: any) => {
    return {
        ...ownProps,
    };
};

export default connect(mapStateToProps)(ChangeIndexButton);
