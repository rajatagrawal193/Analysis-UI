def get_threshold_graphs_inputs():
    return [
        ['graph_type_threshold_graphs', 'value'],
        ['xaxis_threshold_graphs', 'value'],
        ['network_threshold_graphs', 'value'],
        ['device_architecture_threshold_graphs', 'value'],
        ['system_version_threshold_graphs', 'value'],
        ['threshold_threshold_graphs', 'value'],
        ['app_version_threshold_graphs', 'value'],
        ['date-picker', 'start_date'],
        ['date-picker', 'end_date'],
    ]


def get_cache_inputs():
    return {
        'app_open': ['app_version', 'platform', 'system_version', 'network', 'device_architecture',
                     'start_date', 'end_date', 'dist', 'is_cold_start'],
        'screen_open': ['app_version', 'platform', 'system_version', 'network', 'device_architecture',
                        'start_date', 'end_date', 'dist', 'screen_name', 'first_screen_render'],
        'interaction_time': ['app_version', 'platform', 'system_version', 'network', 'device_architecture',
                             'start_date', 'end_date', 'dist', 'screen_name', 'absolute_type'],
        'threshold_graph': ['graph_type', 'xaxis', 'network', 'device_architecture', 'system_version',
                            'threshold', 'app_version', 'start_date', 'end_date']
    }
