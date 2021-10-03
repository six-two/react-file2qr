import { useEffect, useState } from 'react';
import { connect } from 'react-redux';
import QRCode from 'qrcode';
import { ReduxState } from './redux/store';
import { setErrorMessage } from './redux/actions';


const QRCodeImage = (props: Props) => {
    const [data_url, setDataUrl] = useState('');

    useEffect(() => {
        // Side-effect uses `prop` and `state`
        let data = props.file_bytes;
        console.log("data", data);
        if (data) {
            if (data.byteLength > 2000) {
                console.log("TODO implement qr splitting")
                data = data.slice(0, 2000);
            }
            const qr_data = [{
                data: data,
                mode: 'byte'
            }];
            QRCode.toDataURL(qr_data as any, (error, url) => {
                if (error) {
                    setErrorMessage(error.toString());
                } else {
                    console.log("Data URL", url);
                    setDataUrl(url);
                }
            });
        }
    }, [props.file_bytes, setDataUrl]);
    if (data_url) {
        return <a href={data_url} target="_blank" rel="noreferrer" title="Open image in new tab">
            <img src={data_url} alt="Click this QR code to open it in a new tab" />
        </a>
    } else {
        return null;
    }
};

interface Props {
    file_bytes: Uint8Array | null,
}

const mapStateToProps = (state: ReduxState, ownProps: any) => {
    return {
        ...ownProps,
        file_bytes: state.file_bytes,
    };
};

export default connect(mapStateToProps)(QRCodeImage);
