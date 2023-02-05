package fr.sorbonneuniversite.raptormicroservice.models;

import lombok.Data;

import java.util.List;

@Data
public class Trip {
    private long id;
    private List<String> stopTimes;
}
