import { connect } from 'react-redux';
import { ReduxState } from './redux/store';


const QRCodeImage = (props: Props) => {
    if (props.error_message){
        return <div className="error-box">
            {props.error_message}
        </div>
    } else {
        return null;
    }
};

interface Props {
    error_message: string | null,
}

const mapStateToProps = (state: ReduxState, ownProps: any) => {
    return {
        ...ownProps,
        error_message: state.error_message,
    };
};

export default connect(mapStateToProps)(QRCodeImage);
