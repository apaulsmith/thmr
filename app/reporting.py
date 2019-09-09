def patients_as_df(patients):
    df = []
    for patient in patients:
        row = _patient_as_dict(patient)
        df.append(row)

    return df


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


def episodes_as_df(episodes):
    df = []
    for episode in episodes:
        row = _episode_as_dict(episode)
        df.append(row)

    return df


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
