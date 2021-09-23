import React from 'react';
import { Button, Container } from 'semantic-ui-react';
import '../stylesheets/LaunchProfiles.css'

const LaunchProfiles = () => {
    return (
        <div className="button-container">
            <Button color="blue">Download Launch Profile Template</Button>
            <Button color="blue">Create Launch Profile Template</Button>
            <Button color="blue">Download Launch Profile(s)</Button>
            <Button color="blue">Upload Launch Profile Template</Button>
        </div>
    );
};

export default LaunchProfiles;