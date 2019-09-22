from app.util import collection_utils
import pandas as pd
import tempfile

def to_excel(d):
    df = pd.DataFrame.from_dict(d)

    h, path = tempfile.mkstemp(suffix='.xlsx', prefix='report')
    df.to_excel(path,
                index=False)
    return path

def patients_as_dict(patients):
    d = None
    for patient in patients:
        row = _patient_as_dict(patient)
        if d is None:
            d = row
        else:
            collection_utils.append_dicts(d, row)

    return d


def _patient_as_dict(patient):
    row = {
        'name': patient.name,
        'gender': patient.gender,
        'birth_year': patient.birth_year,
        'phone': patient.phone,
        'email': patient.email,
        'address': patient.address
    }

    hospital_dict = _prefix_keys('hospital', _hospital_as_dict(patient.hospital))
    row = _merge_dicts(row, hospital_dict)

    return row


def _hospital_as_dict(hospital):
    return {
        'name': hospital.name,
        'address': hospital.address,
    }


def episodes_as_dict(episodes):
    d = None
    for episode in episodes:
        row = _episode_as_dict(episode)
        if d is None:
            d = row
        else:
            collection_utils.append_dicts(d, row)

    return d


def _episode_as_dict(episode):
    row = {
        'episode_type': episode.episode_type,
        'date': episode.date,
        'comments': episode.comments
    }
    patient_dict = _prefix_keys('patient', _patient_as_dict(episode.patient))
    return _merge_dicts(row, patient_dict)


def _prefix_keys(prefix, d):
    new_d = {}
    for k, v in d.items():
        new_d[prefix + k] = v

    return new_d


def _merge_dicts(d1, d2):
    return {**d1, **d2}
