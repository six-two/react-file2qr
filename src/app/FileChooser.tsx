import React from 'react';
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

    return <Files
    className='files-dropzone'
    onChange={onFilesChange}
    onError={onFilesError}
    accepts={['image/png', '.pdf', 'audio/*']}
    multiple
    maxFiles={3}
    maxFileSize={10000000}
    minFileSize={0}
    clickable
  >
    Drop files here or click to upload
  </Files>
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
