import conn
import dataio
import pandas as pd

def chat(message, space):

    con = conn.gchat()
    spaces = con.spaces().list().execute()

    df = dataio.clean_colnames(pd.DataFrame(spaces["spaces"]))

    df = df[df.displayname == space].reset_index()

    response = (
        con.spaces()
        .messages()
        .create(
            parent=df.loc[0, "name"],
            body={
                "cards": [{
                    "sections": [{
                        "widgets": [{
                            "textParagraph": {
                                "text": message
                            }
                        }]
                    }]
                }]
            },
        ).execute())
    
    return response

def prefect_notify_failure(task, old_state, new_state):
    from datetime import datetime
    now = datetime.now()
    timestamp = now.strftime("%m/%d/%Y %H:%M")
    if new_state.is_failed():
        if 'Trigger was "all_successful"' not in new_state.message:
            chat(
                f"<b>Timestamp:</b> {timestamp}<br><b>Task:</b> {task.name}<br><b>Message:</b> {new_state.message}",
                'Application Errors'
            )