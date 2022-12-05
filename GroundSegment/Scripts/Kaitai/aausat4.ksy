---
meta:
  id: aausat4
  title: AAUSAT4 decoder struct
  endian: be
doc-ref: 'https://github.com/aausat/aausat4_beacon_parser/blob/master/beacon.py'

doc: |
  :field csp_hdr_crc: csp_header.crc
  :field csp_hdr_rdp: csp_header.rdp
  :field csp_hdr_xtea: csp_header.xtea
  :field csp_hdr_hmac: csp_header.hmac
  :field csp_hdr_src_port: csp_header.src_port
  :field csp_hdr_dst_port: csp_header.dst_port
  :field csp_hdr_destination: csp_header.destination
  :field csp_hdr_source: csp_header.source
  :field csp_hdr_priority: csp_header.priority
  :field subsystems_valid: csp_data.csp_payload.valid
  :field eps_boot_count: csp_data.csp_payload.eps.boot_count
  :field eps_boot_cause: csp_data.csp_payload.eps.boot_cause
  :field eps_uptime: csp_data.csp_payload.eps.uptime
  :field eps_rt_clock: csp_data.csp_payload.eps.rt_clock
  :field eps_ping_status: csp_data.csp_payload.eps.ping_status
  :field eps_subsystem_selfstatus: csp_data.csp_payload.eps.subsystem_selfstatus
  :field eps_battery_voltage: csp_data.csp_payload.eps.battery_voltage
  :field eps_cell_diff: csp_data.csp_payload.eps.cell_diff
  :field eps_battery_current: csp_data.csp_payload.eps.battery_current
  :field eps_solar_power: csp_data.csp_payload.eps.solar_power
  :field eps_temp: csp_data.csp_payload.eps.temp
  :field eps_pa_temp: csp_data.csp_payload.eps.pa_temp
  :field eps_main_voltage: csp_data.csp_payload.eps.main_voltage
  :field com_boot_count: csp_data.csp_payload.com.boot_count
  :field com_boot_cause: csp_data.csp_payload.com.boot_cause

seq:
  - id: csp_header
    type: csp_header_t
  - id: csp_data
    type: csp_data_t
types:
  csp_header_t:
    seq:
      - id: csp_flags
        type: u1
        repeat: expr
        repeat-expr: 4
    instances:
      crc:
        value: >-
          (
          (csp_flags[0])
          ) & 0x1
      rdp:
        value: >-
          (
          (
          (csp_flags[0])
          ) >> 1
          ) & 0x1
      xtea:
        value: >-
          (
          (
          (csp_flags[0])
          ) >> 2
          ) & 0x1
      hmac:
        value: >-
          (
          (
          (csp_flags[0])
          ) >> 3
          ) & 0x1
      reserved:
        value: >-
          (
          (csp_flags[0])
          ) >> 4
      src_port:
        value: >-
          (
          (csp_flags[1])
          ) & 0x3F
      dst_port:
        value: >-
          (
          (
          (csp_flags[1]) |
          (csp_flags[2] << 8)
          ) >> 6
          ) & 0x3F
      destination:
        value: >-
          (
          (
          (csp_flags[2]) |
          (csp_flags[3] << 8)
          ) >> 4
          ) & 0x1F
      source:
        value: >-
          (
          (
          (csp_flags[3])
          ) >> 1
          ) & 0x1F
      priority:
        value: >-
          (
          (csp_flags[3])
          ) >> 6
  csp_data_t:
    seq:
      - id: csp_payload
        type:
          switch-on: frame_length
          cases:
            88: aausat4_beacon_t
    instances:
      frame_length:
        value: _io.size

  # The beacon format is as follows:
  #  [ 1 byte | 20 bytes  | 10 bytes | 7 bytes  | 6 bytes  | 20 bytes  | 20 bytes  ]
  #  [ Valid  |    EPS    |    COM   |   ADCS1  |  ADCS2   |   AIS1    |   AIS2    ]
  aausat4_beacon_t:
    seq:
      - id: valid
        type: u1
      - id: eps
        type: eps_t
        size: 20
      - id: com
        type: com_t
        size: 10
      - id: adcs1
        type: adcs1_t
      - id: adcs2
        type: adcs2_t
      - id: ais1
        type: ais1_t
      - id: ais2
        type: ais2_t
      - id: unparsed
        size-eos: true
  eps_t:
    seq:
      - id: boot_count_raw
        type: u2
      - id: uptime
        type: u4
      - id: rt_clock
        type: u4
      - id: ping_status
        type: u1
      - id: subsystem_selfstatus
        type: u2
      - id: battery_voltage
        type: u1
      - id: cell_diff
        type: s1
      - id: battery_current
        type: s1
      - id: solar_power
        type: u1
      - id: temp
        type: s1
      - id: pa_temp
        type: s1
      - id: main_voltage
        type: s1
    instances:
      boot_count:
        value: 'boot_count_raw & 0x1FFF'
      boot_cause:
        value: '(boot_count_raw & 0xE000) >> 13'
  com_t:
    seq:
      - id: boot_count_raw
        type: u2
    instances:
      boot_count:
        value: 'boot_count_raw & 0x1FFF'
      boot_cause:
        value: '(boot_count_raw & 0xE000) >> 13'
  adcs1_t:
    seq:
      - id: unparsed
        size: 7
  adcs2_t:
    seq:
      - id: unparsed
        size: 6
  ais1_t:
    seq:
      - id: unparsed
        size: 20
  ais2_t:
    seq:
      - id: unparsed
        size: 20
