## Information

This is a basic streamlit data application for [Keboola platform](). Application provides a simple button for external users to trigger existing Keboola flow.

![Keboola Flow Trigger in Streamlit](/images/image_03.png)

## How to use it

### Token rights
Please make sure the token you create has access to:
 - keboola.flow component
 - all components used by the flow
 - all tables used by the flow

 *Note: This is a security perimeter dictated by the token authentication.*

 Example:
![token rights](/images/image_02.png)

 ### Packages needed
 - requests

### Application secret
 - keboola_token (use encrypted field)
 - config_id (use flow id)

 Example:
![token rights](/images/image_01.png)

## Documentation
Please see [official Keboola documentation on Data Applications](https://help.keboola.com/components/data-apps/).

