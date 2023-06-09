package io.cloudadc.nginx.dumpplane.hander;

import java.util.List;

import io.cloudadc.nginx.dumpplane.model.Configuration;

public interface Hander {
	
	public static final String DISK_PATH = "data";
	
	public static final String DUMP_PATH = ".dumpplane";
	
	public static final String DB_NAME = "nginx";
	
	public void execute() throws Exception;
	
	public void execute(Configuration config) throws Exception;
	
	public void execute(List<Configuration> list ) throws Exception;
	
	public void close() throws Exception;

}
