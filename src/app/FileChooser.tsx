import { connect } from 'react-redux';
import Files from 'react-files';
import { ReduxState } from './redux/store';
import { setFile } from './redux/actions';


const QRCodeImage = (props: Props) => {
    const onFilesChange = (files: any) => {
        const file_name = files[0];
        console.log('Selected file:', file_name);

        const reader = new FileReader();
        reader.readAsArrayBuffer(file_name);
        reader.onloadend = function (evt) {
            if (evt.target && evt.target.readyState === FileReader.DONE) {
                var arrayBuffer = evt.target.result;
                if (arrayBuffer) {
                    const array = new Uint8Array(arrayBuffer as any);
                    setFile(file_name.name, array);
                }
            }
        }
    }

    const onFilesError = (error: any, file: any) => {
        console.log('error code ' + error.code + ': ' + error.message)
    };

    const text = props.file_name ?
        `File uploaded: '${props.file_name}'. Drop a different file here or click here to change the file`
        : "Drop a file here or click here to get started";

    return <div>
        <Files
            className='files-dropzone'
            onChange={onFilesChange}
            onError={onFilesError}
            multiple={false}
            maxFileSize={10000000}
            minFileSize={0}
            clickable>
            {text}
        </Files>
    </div>
};

interface Props {
    file_name: string | null,
}

const mapStateToProps = (state: ReduxState, ownProps: any) => {
    return {
        ...ownProps,
        file_name: state.file_name,
    };
};

export default connect(mapStateToProps)(QRCodeImage);
