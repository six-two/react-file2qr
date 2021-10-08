import { useEffect, useState } from 'react';
import { connect } from 'react-redux';
import QRCode from 'qrcode';
import { ChunkState, ReduxState } from './redux/store';
import { setErrorMessage } from './redux/actions';
import { addQrHeadersToDataSlice, HashedData } from './encoders/QrHeaders';


const generateQRCode = (data: Uint8Array | undefined, options: any, setDataUrl: (data_url: string) => void) => {
    console.debug("Data with header", data);

    const qr_data = [{
        data: data,
        mode: 'byte',
    }] as any;
    //@ts-ignore
    QRCode.toDataURL(qr_data, options, (error, url) => {
        if (error) {
            setDataUrl("");
            setErrorMessage(error.toString());
        } else {
            console.log("Data URL", url);
            setDataUrl(url);
            setErrorMessage("");
        }
    });
};

const QRCodeImage = (props: Props) => {
    const [data_url, setDataUrl] = useState('');

    useEffect(() => {
        const options = { errorCorrectionLevel: props.error_correction_level };
        if (props.file_export_bytes) {
            const size = props.chunks.size
            const start_index = props.chunks.index * size;
            const end_index = Math.min(start_index + size, props.file_export_bytes.data.length);
            const data_with_headers = addQrHeadersToDataSlice(props.file_export_bytes, start_index, end_index);

            generateQRCode(data_with_headers, options, setDataUrl);
        } else {
            setDataUrl("");
            setErrorMessage("No data to create a QR code from");
        }

    }, [props.file_export_bytes, props.error_correction_level, props.chunks, setDataUrl]);
    if (data_url) {
        return <a href={data_url} target="_blank" rel="noreferrer" title="Open image in new tab">
            <img src={data_url} alt="Click this QR code to open it in a new tab" />
        </a>
    } else {
        return null;
    }
};

interface Props {
    file_export_bytes?: HashedData,
    error_correction_level: string,
    chunks: ChunkState,
}

const mapStateToProps = (state: ReduxState, ownProps: any) => {
    return {
        ...ownProps,
        file_export_bytes: state.file?.serialized,
        error_correction_level: state.error_correction_level,
        chunks: state.chunks,
    };
};

export default connect(mapStateToProps)(QRCodeImage);
