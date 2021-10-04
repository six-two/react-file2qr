import { useEffect, useState } from 'react';
import { connect } from 'react-redux';
import QRCode from 'qrcode';
import { ReduxState } from './redux/store';
import { setErrorMessage } from './redux/actions';
import { addQrHeadersToDataSlice, HashedData } from './encoders/QrHeaders';


const QRCodeImage = (props: Props) => {
    const [data_url, setDataUrl] = useState('');

    useEffect(() => {
        // Side-effect uses `prop` and `state`
        let data = props.result_bytes;
        console.log("data", data);
        if (data) {
            let error_message = "";
            if (data.byteLength > 2000) {
                error_message = "TODO implement qr splitting. The currect code is capped";
                data = data.slice(0, 2000);
            }
            const hashed_data = new HashedData(data);
            const data_with_headers = addQrHeadersToDataSlice(hashed_data, 0, data.length);
            console.debug("Data with header", data_with_headers);

            const options = { errorCorrectionLevel: props.error_correction_level };;
            const qr_data = [{
                data: data_with_headers,
                mode: 'byte'
            }];
            //@ts-ignore
            QRCode.toDataURL(qr_data as any, options, (error, url) => {
                if (error) {
                    setDataUrl("")
                    setErrorMessage(error.toString());
                } else {
                    console.log("Data URL", url);
                    setDataUrl(url);
                    setErrorMessage(error_message);
                }
            });
        }
    }, [props.result_bytes, props.error_correction_level, setDataUrl]);
    if (data_url) {
        return <a href={data_url} target="_blank" rel="noreferrer" title="Open image in new tab">
            <img src={data_url} alt="Click this QR code to open it in a new tab" />
        </a>
    } else {
        return null;
    }
};

interface Props {
    result_bytes: Uint8Array | null,
    error_correction_level: string,
}

const mapStateToProps = (state: ReduxState, ownProps: any) => {
    return {
        ...ownProps,
        result_bytes: state.result_bytes,
        error_correction_level: state.error_correction_level,
    };
};

export default connect(mapStateToProps)(QRCodeImage);
