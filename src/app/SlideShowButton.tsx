import { useEffect } from 'react';
import { connect } from 'react-redux';
import { ReduxState, SlideShowState } from './redux/store';
import { setChunkIndex, setSlideShowEnabled } from './redux/actions';
import { INDEX_NEXT } from './redux/constants';


const SlideShowButton = (props: Props) => {
    const time = props.slide_show.time_in_ms;
    const enabled = props.multiple_codes && props.slide_show.enabled;
    useEffect(() => {
        if (enabled) {
            const timer = setInterval(() => {
                setChunkIndex(INDEX_NEXT);
            }, time);
            // clearing interval
            return () => clearInterval(timer);
        }
    }, [time, enabled]);

    if (props.multiple_codes) {
        const text = props.slide_show.enabled ? "Pause" : "Play";
        const toggleEnabled = () => setSlideShowEnabled(!props.slide_show.enabled);
        return <button
            onClick={toggleEnabled}>
            {text}
        </button>
    } else {
        return null;
    }
};

interface Props {
    slide_show: SlideShowState,
    multiple_codes: boolean,
}

const mapStateToProps = (state: ReduxState, ownProps: any) => {
    return {
        ...ownProps,
        slide_show: state.slide_show,
        multiple_codes: state.chunks.max_index > 0,
    };
};

export default connect(mapStateToProps)(SlideShowButton);
