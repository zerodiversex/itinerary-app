package fr.sorbonneuniversity.gateway.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
@Data
public class Stop {
    public long stopId;

    public String stopName;

    public String stopDesc;

    public String stopLat;

    public String stopLon;
}
