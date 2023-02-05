package fr.sorbonneuniversity.gateway.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
@Data
public class Journey {
    public long stopId;

    public String footpath;

    public String walkingTime;

    public String endTime;

    public String startTime;

    public String transport;
}
